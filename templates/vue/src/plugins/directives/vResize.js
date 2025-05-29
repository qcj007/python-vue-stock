
import { throttle } from "lodash-es";

const vResize = {
  mounted(el, binding) {
    // el为绑定的元素，binding为绑定给指令的对象
    let width = ""
    let height = ""
    el.__resizeObserver__ = new ResizeObserver(throttle((entries) => {
      for (let entry of entries) {
        let curWidth = entry.target.clientWidth;
        let curHeight = entry.target.clientHeight;
        if (width !== curWidth || height !== curHeight) {
          width = curWidth;
          height = curHeight;
          binding.value({ width, height }); // 关键(这传入的是函数,所以执行此函数)
        }
      }
    }, 40));
    el.__resizeObserver__.observe(el);
  },
  unmounted(el) {
    el.__resizeObserver__.disconnect();
    el.__resizeObserver__ = null;
  },
}

export default vResize