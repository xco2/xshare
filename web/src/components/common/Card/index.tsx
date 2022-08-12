import { type ExtractPropTypes } from 'vue'
import clx from 'classnames'

import styles from './index.module.less'

const cardProps = {
  title: String,
  subtitle: String,
  extra: String,
  headerBordered: Boolean,
  ghost: Boolean,
  titleClassName: String,
  titleStyles: Object,
  bodyStyle: Object,
  class: String,
}

export type CardProps = ExtractPropTypes<typeof cardProps>

export default defineComponent({
  name: 'CommonCard',
  props: cardProps,
  setup(props, { slots }) {
    const renderTitle = () => {
      if (slots.title) {
        return slots.title()
      }
      if (props.title) {
        return <div class={styles['common-card-title']}>{props.title}</div>
      }
    }
    const renderSubtitle = () => {
      if (slots.subtitle) {
        return slots.subtitle()
      }
      if (props.subtitle) {
        return <div class={styles['common-card-subtitle']}>{props.subtitle}</div>
      }
    }

    const renderExtra = () => {
      if (slots.extra) {
        return slots.extra()
      }
      if (props.extra) {
        return <div class={styles['common-card-extra']}>{props.extra}</div>
      }
    }

    return () => {
      const showHeader = computed(() => !!(props.title || props.subtitle || props.extra))

      return (
        <div class={clx(styles['common-card-container'], props.class)}>
          {showHeader && (
            <div
              class={clx(
                styles['common-card-header'],
                props.headerBordered && styles['common-card-headerBordered'],
              )}
              style={{ ...(props?.titleStyles ?? {}) }}
            >
              <div class="flex justify-between flex-nowrap">
                <div class={clx(styles['common-card-title'], props.titleClassName)}>
                  {renderTitle()}
                </div>
                <div class={clx(styles['common-card-extra'])}>{renderExtra()}</div>
              </div>
              {renderSubtitle()}
            </div>
          )}
          <div
            class={clx(!props.ghost && styles['common-card-body'])}
            style={{
              ...props?.bodyStyle,
            }}
          >
            {slots.default?.()}
          </div>
        </div>
      )
    }
  },
})
