export function frontSchedulingEnterView(
  container: HTMLDivElement,
  target: HTMLDivElement,
  scaleNum = 4,
  onSuccess?: (top: number) => void,
) {
  const containerCenter = getDOMCenter(container)
  const top = getElementTop(target)
  const left = getElementLeft(target)

  const scalecha = scaleNum - 4
  const top_ =
    containerCenter.top -
    (target.clientHeight * (4 / 2)) / 2 +
    (target.clientHeight * (scalecha / 2)) / 2
  const left_ =
    containerCenter.left - (target.clientWidth * (4 / 2)) / 2 + target.clientWidth * (scalecha / 2)

  const k = (top_ - top) / (left_ - left)
  const distance = Math.sqrt((top_ - top) ** 2 + (left_ - left) ** 2)

  let targetX = left
  let targetOpacity = 0.6
  let targetRotateY = 60
  let targetScale = 1

  const hz = 60
  const runTime = 0.45

  const distanceSecond = distance / (hz * runTime)
  const distanceOpacity = 1 / (hz * runTime)
  const distanceRotateY = 60 / (hz * runTime)
  const distanceScale = scaleNum / (hz * runTime)

  const stepX = distanceSecond
  const stepOpacity = distanceOpacity
  const stepRotateY = distanceRotateY
  const scale = distanceScale

  const runPathFn = (x: number) => {
    const y = k * (x - left_) + top_
    target.style.top = `${y}px`
    target.style.left = `${x}px`
    targetX += stepX
    targetRotateY -= stepRotateY
    targetScale += scale

    if (targetOpacity <= 1) {
      targetOpacity += stepOpacity
      target.style.opacity = `${targetOpacity > 1 ? 1 : targetOpacity}`
    }
    if (targetRotateY > 0 || scale <= scaleNum) {
      const realscale = targetScale > scaleNum ? scaleNum : targetScale
      target.style.transform = `rotate3d(0,1,0,${
        targetRotateY < 0 ? 0 : targetRotateY
      }deg) scale3d(${realscale},${realscale},${realscale})`
    }

    if (targetX <= left_) requestAnimationFrame(() => runPathFn(targetX))
    else {
      target.style.opacity = '1'
      target.style.transform = `rotate3d(0,1,0,0deg) scale(${scaleNum})`
      onSuccess?.(top_)
    }
  }

  runPathFn(targetX)
}

export function getDOMCenter(target: HTMLDivElement) {
  const rect = target.getBoundingClientRect()
  //中心位置
  const center = {
    left: rect.left + (rect.right - rect.left) / 2,
    top: rect.top + (rect.bottom - rect.top) / 2,
  }
  const scrollLeft = document.body.scrollLeft || document.documentElement.scrollLeft
  const scrollTop = document.body.scrollTop || document.documentElement.scrollTop
  center.left = scrollLeft + center.left
  center.top = scrollTop + center.top

  return center
}

function getElementLeft(element: any) {
  let actualLeft = element.offsetLeft
  let current = element.offsetParent

  while (current !== null) {
    actualLeft += current.offsetLeft
    current = current.offsetParent
  }

  return actualLeft
}

function getElementTop(element: any) {
  let actualTop = element.offsetTop
  let current = element.offsetParent

  while (current !== null) {
    actualTop += current.offsetTop
    current = current.offsetParent
  }

  return actualTop
}
