/**
 * @description: v-hover 指令，监听鼠标划过的时候并执行相应的函数
 * @param {Function} onMouseover 鼠标移入元素触发
 * @param {Function} mouseout 鼠标移出元素触发
 * @param {Function} mouseenter 鼠标移入元素/子元素触发 
 * @param {Function} mouseleave 鼠标移出元素/子元素触发 
 * @param {Number} overInterval  触发时间 default:0
 * @param {Number} outInterval  触发时间 default:0
 * @param {Number} enterInterval  触发时间 default:0
 * @param {Number} leaveInterval  触发时间 default:0
 * @param {any} $event  入参 
 * @param {boolean} isBreak  true 分割 | false 全局
 */
var intervalElDefault = {}
// 清除定时器
const clearInterval = (intervalEl) => {
  clearTimeout(intervalEl.__vueDerectiveMouseoverInterval__);
  intervalEl.__vueDerectiveMouseoverInterval__ = null;

  clearTimeout(intervalEl.__vueDerectiveMouseoutInterval__);
  intervalEl.__vueDerectiveMouseoutInterval__ = null;

  clearTimeout(intervalEl.__vueDerectiveMouseenterInterval__);
  intervalEl.__vueDerectiveMouseenterInterval__ = null;

  clearTimeout(intervalEl.__vueDerectiveMouseleaveInterval__);
  intervalEl.__vueDerectiveMouseleaveInterval__ = null;
}

export const vMouseHover = {
  mounted(el, binding) {
    const bindingValue = binding?.value || {}
    const { onMouseover, onMouseout, onMouseenter, onMouseleave, $event: event, isBreak } = bindingValue
    const intervalEl = isBreak ? el : intervalElDefault

    // 鼠标移入元素/子元素触发
    intervalEl.__vueDerectiveMouseoverFn__ = function __vueDerectiveMouseoverFn__() {
      if (!intervalEl.__vueDerectiveMouseoverInterval__ && onMouseover) {
        clearInterval(intervalEl)
        const intervalTime = bindingValue?.overInterval || 0;
        intervalEl.__vueDerectiveMouseoverInterval__ = setTimeout(() => {
          onMouseover(event)
        }, intervalTime);
      }
    };

    // 鼠标移出元素/子元素触发
    intervalEl.__vueDerectiveMouseoutFn__ = function __vueDerectiveMouseoutFn__() {
      if (!intervalEl.__vueDerectiveMouseoutInterval__ && onMouseout) {
        clearInterval(intervalEl)
        const intervalTime = bindingValue?.outInterval || 0;
        intervalEl.__vueDerectiveMouseoutInterval__ = setTimeout(() => {
          onMouseout(event)
        }, intervalTime);
      }
    };

    // 鼠标移入元素
    intervalEl.__vueDerectiveMouseenterFn__ = function __vueDerectiveMouseenterFn__() {
      if (!intervalEl.__vueDerectiveMouseenterInterval__ && onMouseenter) {
        clearInterval(intervalEl)
        const intervalTime = bindingValue?.enterInterval || 0;
        intervalEl.__vueDerectiveMouseenterInterval__ = setTimeout(() => {
          onMouseenter(event)
        }, intervalTime);
      }
    };

    // 鼠标移除元素
    intervalEl.__vueDerectiveMouseleaveFn__ = function __vueDerectiveMouseleaveFn__() {
      if (!intervalEl.__vueDerectiveMouseleaveInterval__ && onMouseleave) {
        clearInterval(intervalEl)
        const intervalTime = bindingValue?.leaveInterval || 0;
        intervalEl.__vueDerectiveMouseleaveInterval__ = setTimeout(() => {
          onMouseleave(event)
        }, intervalTime);
      }
    };

    el.addEventListener("mouseover", intervalEl.__vueDerectiveMouseoverFn__);
    el.addEventListener("mouseout", intervalEl.__vueDerectiveMouseoutFn__);
    el.addEventListener("mouseleave", intervalEl.__vueDerectiveMouseleaveFn__);
    el.addEventListener("mouseenter", intervalEl.__vueDerectiveMouseenterFn__);
  },
  unmounted(el, binding) {
    const intervalEl = binding?.value?.isBreak ? el : intervalElDefault
    el.removeEventListener("mouseover", intervalEl.__vueDerectiveMouseoverFn__);
    el.removeEventListener("mouseout", intervalEl.__vueDerectiveMouseoutFn__);
    el.removeEventListener("mouseleave", intervalEl.__vueDerectiveMouseleaveFn__);
    el.removeEventListener("mouseenter", intervalEl.__vueDerectiveMouseenterFn__);
    clearInterval(intervalEl)
  },
};


export default vMouseHover