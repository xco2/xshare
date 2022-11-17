import cv2
import numpy as np
import os
from flask import Flask, request, render_template, session, jsonify, Response
import time


def generate_chessboard(cube_cm=2., pattern_size=(8, 6), scale=37.79527559055118):
    """
    generate chessboard image with given cube length, which adapts to A4 paper print
    :param cube_cm: float, single cube length in cm
    :param pattern_size: (x, y), the number of points in x, y axes in the chessboard
    :param scale: float, scale pixel/cm in A4 paper
    """
    # convert cm to pixel
    cube_pixel = cube_cm * scale
    width = round(pattern_size[0] * cube_cm * scale)
    height = round(pattern_size[1] * cube_cm * scale)

    # generate canvas
    image = np.zeros([width, height, 3], dtype=np.uint8)
    image.fill(255)
    color = (255, 255, 255)
    fill_color = 0
    # drawing the chessboard
    for j in range(0, height + 1):
        y = round(j * cube_pixel)
        for i in range(0, width + 1):
            x0 = round(i * cube_pixel)
            y0 = y
            rect_start = (x0, y0)

            x1 = round(x0 + cube_pixel)
            y1 = round(y0 + cube_pixel)
            rect_end = (x1, y1)
            cv2.rectangle(image, rect_start, rect_end, color, 1, 0)
            image[y0:y1, x0:x1] = fill_color
            if width % 2:
                if i != width:
                    fill_color = (0 if (fill_color == 255) else 255)
            else:
                if i != width + 1:
                    fill_color = (0 if (fill_color == 255) else 255)

    # add border around the chess
    chessboard = cv2.copyMakeBorder(image, 30, 30, 30, 30, borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255))
    # visualize
    win_name = "chessboard"
    # cv2.imshow(win_name, chessboard)
    # cv2.waitKey(0)
    return cv2.cvtColor(chessboard, cv2.COLOR_BGR2RGB)


def load_imgs(img_dir):
    assert os.path.isdir(img_dir), 'Path {} is not a dir'.format(img_dir)
    imagenames = os.listdir(img_dir)
    imgs = []
    for imagename in imagenames:
        if os.path.splitext(imagename)[-1] not in ['.jpg', '.png', '.bmp', '.tiff', '.jpeg']:
            continue
        img_path = os.path.join(img_dir, imagename)
        # img = cv2.imread(img_path)
        img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
        imgs.append(img)
    return imgs


def calib_camera(imgs: list, pattern_size: [tuple, list] = (8, 6), draw_points: bool = False) -> tuple:
    """
    calibrate camera
    :param imgs: 棋盘照片列表
    :param pattern_size: (x, y), 棋盘中x、y轴上的点数
    :param draw_points: bool, 是否绘制棋盘点
    :return: k_cam, dist_coeffs, dst:矫正样例, draw_points_imgs:绘制了棋盘点的图
    """
    # store 3d object points and 2d image points from all the images
    object_points = []
    image_points = []

    # 3d object point coordinate
    xl = np.linspace(0, pattern_size[0], pattern_size[0], endpoint=False)
    yl = np.linspace(0, pattern_size[1], pattern_size[1], endpoint=False)
    xv, yv = np.meshgrid(xl, yl)
    object_point = np.insert(np.stack([xv, yv], axis=-1), 2, 0, axis=-1).astype(np.float32).reshape([-1, 3])
    # set termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    draw_points_imgs = []
    for img in imgs:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # find chessboard points
        ret, corners = cv2.findChessboardCorners(img_gray, patternSize=pattern_size)
        if ret:
            # add the corresponding 3d points to the summary list
            object_points.append(object_point)
            # if chessboard points are found, refine them to SubPix level (pixel location in float)
            corners_refined = cv2.cornerSubPix(img_gray, corners, (11, 11), (-1, -1), criteria)
            # add the 2d chessboard points to the summary list
            image_points.append(corners.reshape([-1, 2]))
            # visualize the points
            if draw_points:
                cv2.drawChessboardCorners(img, pattern_size, corners_refined, ret)
                if img.shape[0] * img.shape[1] > 1e6:
                    scale = round((1. / (img.shape[0] * img.shape[1] // 1e6)) ** 0.5, 3)
                    img_draw = cv2.resize(img, (0, 0), fx=scale, fy=scale)
                else:
                    img_draw = img

                draw_points_imgs.append(img_draw)
                # cv2.imshow('img', img_draw)
                # cv2.waitKey(0)

    assert len(image_points) > 0, 'Cannot find any chessboard points, maybe incorrect pattern_size has been set'
    # calibrate the camera, note that ret is the rmse of reprojection error, ret=1 means 1 pixel error
    reproj_err, k_cam, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(object_points,
                                                                       image_points,
                                                                       img_gray.shape[::-1],
                                                                       None,
                                                                       None,
                                                                       criteria=criteria)

    dst = cv2.undistort(img, k_cam, dist_coeffs)
    # cv2.imshow("dst", cv2.resize(dst, None, fx=1 / 3, fy=1 / 3))
    # print(reproj_err, "\n", k_cam, "\n", dist_coeffs)
    return k_cam, dist_coeffs, dst, draw_points_imgs


def upload_chessboard_img(save_path) -> [bool, str]:
    """
    上传棋盘照片
    :param save_path:保存的目录
    :return: 成功返回保存的目录,失败返回False
    """
    random_dir_name = "{0:0>}".format(np.random.randint(1, 9999))
    save_path_r = os.path.join(save_path, random_dir_name)
    while os.path.exists(save_path_r):
        random_dir_name = "{0:0>}".format(np.random.randint(1, 9999))
        save_path_r = os.path.join(save_path, random_dir_name)
    os.mkdir(save_path_r)

    file_objs = request.files.getlist("upload_file")
    if len(file_objs) < 20:
        return False
    for file_id, file_obj in enumerate(file_objs):
        file_bytes = file_obj.read()
        file_name = os.path.join(save_path_r, file_obj.filename)
        with open(file_name, "wb") as f:
            f.write(file_bytes)
    return save_path_r


if __name__ == '__main__':
    generate_chessboard()
    imgs = load_imgs(r"D:\啊这\py项目\拼接图片\imgs\calibration\chess")
    k_cam, dist_coeffs, dst, draw_points_imgs = calib_camera(imgs)
    print(k_cam)
    print(dist_coeffs)

    """
    [[2.87621783e+03 0.00000000e+00 9.58328196e+02]
    [0.00000000e+00 2.89709485e+03 5.39127066e+02]
    [0.00000000e+00 0.00000000e+00 1.00000000e+00]] 
    [[-5.39893810e-01 -4.50841069e+00 -2.59781416e-03  1.32162790e-02
   2.84612311e+00]]
    """

    cv2.waitKey(0)
