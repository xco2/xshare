<template>
  <div class="container" ref="containerRef">
    <div
      class="small-figure"
      v-for="item in images"
      :key="item.key"
      :style="{
        // background: `url(${item.view})`,
        backgroundColor: '#fff',
        backgroundSize: 'cover',
        top: `${item.top}px`,
        filter: item.active ? 'none' : 'grayscale(50%)',
      }"
      :ref="
        (ref) => {
          setFigureRefs(ref)
        }
      "
      @click="() => (item.active ? null : handleClick(item.key))"
    >
      <div
        :style="{
          width: '100%',
          height: '100%',
          overflow: 'scroll',
          transform: `scale(${zoomValue})`,
          position: 'absolute',
          padding: '24px',
          paddingTop: `${30 + scaleNumAdd * 20}px`,
          paddingLeft: `8px`,
          transformOrigin: 'top left',
        }"
        class="terminal"
      >
        <Preview :text="item.text" />
      </div>

      <!-- </Terminal> -->
    </div>
  </div>
  <div class="bar">台前调度</div>
</template>

<script lang="ts" setup>
  import img from '@/assets/1.png'

  import { frontSchedulingEnterView } from './frontScheduling'
  import Preview from './Preview.vue'

  const containerRef = ref()

  const figureRefs = ref<any[]>([])

  const activeKey = ref(0)

  const scaleNum = ref(5)

  const scaleNumAdd = ref(0)

  const setFigureRefs = (el: any) => {
    if (el) figureRefs.value.push(el)
  }

  const images = ref(
    [
      {
        key: 0,
        view: img,
        active: false,
        text: '我是1',
      },
      {
        key: 1,
        view: img,
        active: false,
        text: '我是2',
      },
      {
        key: 2,
        view: img,
        active: false,
        text: '我是3',
      },
      {
        key: 3,
        view: img,
        active: false,
        text: '我是4',
      },
      {
        key: 4,
        view: img,
        active: false,
        text: '我是5',
      },
    ]?.map((item, index) => ({
      ...item,
      top: index * (100 + 24) + 24,
    })),
  )

  onMounted(() => {
    scaleNum.value = (window.screen.availWidth * 5.3) / 1920

    scaleNumAdd.value = (window.screen.availWidth * 0.08) / 1920
  })

  const zoomValue = computed(() => 1 / scaleNum.value)

  const returnList = () => {
    const target: HTMLDivElement = figureRefs.value[activeKey.value]
    const top = (images.value.length - 1) * (100 + 24) + 24
    target.style.transform = 'rotate3d(0,1,0,60deg) scale3d(1,1,1)'
    target.style.top = `${top}px`
    target.style.left = `0px`
    images.value = images.value?.map((item) => {
      if (item.key === activeKey.value) {
        return {
          ...item,
          top,
          active: false,
        }
      }
      return item
    })
  }

  const handleClick = (key: number) => {
    const activeTarget = images.value.find((i) => i.active === true)
    if (activeTarget) {
      returnList()
    }
    activeKey.value = key
    const targetTop = images.value.find((item) => item.key === key)!.top
    frontSchedulingEnterView(containerRef.value, figureRefs.value[key], scaleNum.value, (top) => {
      images.value = images.value.map((item) => {
        if (item.top < targetTop)
          return {
            ...item,
            active: false,
          }
        if (item.top > targetTop)
          return {
            ...item,
            active: false,
            top: item.top - (100 + 24),
          }

        return {
          ...item,
          active: true,
          top,
        }
      })
    })
  }
  // Small figure
</script>

<style scoped lang="less">
  .container {
    width: 100%;
    height: 90%;
    position: absolute;
    perspective: 1500px;
    // perspective-origin: center center;

    .small-figure {
      position: absolute;
      left: 0;
      height: 100px;
      width: 180px;
      // transition: all 0.3s;
      opacity: 0.6;
      transform: rotate3d(0, 1, 0, 60deg);
      border-radius: 4px;
      overflow: hidden;
      filter: grayscale(50%);
    }

    .small-figure:hover {
      transform: scale3d(1.1, 1.1, 1.1) rotate3d(0, 1, 0, 60deg);
      opacity: 1;
      filter: none;
    }
  }

  .terminal {
    height: 100%;
    line-height: 16px;
    border-radius: 7px;
    position: relative;
    // box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.05), 0 0 30px 1px rgba(0, 0, 0, 0.15);
    width: 100%;
    max-width: 100%;
    overflow: scroll;
    // padding-bottom: 0;
    // margin-bottom: 32px;
  }

  .terminal::after {
    content: '';
    position: fixed;
    top: 12px;
    left: 10px;
    width: 12px;
    height: 12px;
    z-index: 100;
    background: #f95c5b;
    border-radius: 7px;
    box-shadow: 0 0 0 1px #da3d42, 22px 0 0 0 #fabe3b, 22px 0 0 1px #ecb03e, 44px 0 0 0 #38cd46,
      44px 0 0 1px #2eae32;
  }

  .close {
    width: 12px;
    height: 12px;
    background: #f95c5b;
    border-radius: 100%;
  }

  .bar {
    position: absolute;
    width: 100%;
    bottom: 10%;
  }
</style>
