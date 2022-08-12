import './index.less'

export default defineComponent({
  setup(props, { slots }) {
    return () => (
      <>
        <div class="common-page-container">{slots.default?.()}</div>
        {/* <div class="h-16"></div> */}
      </>
    )
  },
})
