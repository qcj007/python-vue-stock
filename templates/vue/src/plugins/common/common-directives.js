export const vResize = {
  bind(el, binding) {
    // el为绑定的元素，binding为绑定给指令的对象
    let width = "",
      height = "";
    el.__resizeObserver__ = new ResizeObserver((entries) => {
      for (let entry of entries) {
        let curWidth = entry.target.clientWidth;
        let curHeight = entry.target.clientHeight;
        if (width !== curWidth || height !== curHeight) {
          width = curWidth;
          height = curHeight;
          binding.value({ width: `${width}px`, height: `${height}px` }); // 关键(这传入的是函数,所以执行此函数)
        }
      }
    });
    el.__resizeObserver__.observe(el);
  },
  unbind(el) {
    el.__resizeObserver__.disconnect();
    el.__resizeObserver__ = null;
  },
};

/**
 * @description: v-mouse-hover 指令，监听鼠标划过的时候并执行相应的函数
 * @param {Function} onMouseover 鼠标进入
 * @param {Function} onMouseleave 鼠标划出
 * @param {Number} interval 触发时间 default:500
 */
export const vMouseHover = {
  bind(el, binding) {
    el.__vueDerectiveMouseoverFn__ = function __vueDerectiveMouseoverFn__() {
      const intervalTime = binding?.value?.interval || 500;
      if (!el.__vueDerectiveMouseoverInterval__ && binding?.value?.onMouseover) {
        el.__vueDerectiveMouseoverInterval__ = setTimeout(binding?.value?.onMouseover, intervalTime);
      }
    };
    el.__vueDerectiveMouseleaveFn__ = function __vueDerectiveMouseleaveFn__() {
      binding?.value?.onMouseleave && binding?.value?.onMouseleave();
      clearTimeout(el.__vueDerectiveMouseoverInterval__);
      el.__vueDerectiveMouseoverInterval__ = null;
    };

    el.addEventListener("mouseover", el.__vueDerectiveMouseoverFn__);
    el.addEventListener("mouseleave", el.__vueDerectiveMouseleaveFn__);
  },
  unbind(el) {
    el.removeEventListener("mouseover", el.__vueDerectiveMouseoverFn__);
    el.removeEventListener("mouseleave", el.__vueDerectiveMouseleaveFn__);
    clearTimeout(el.__vueDerectiveMouseoverInterval__);
    el.__vueDerectiveMouseoverInterval__ = null;
    el.__vueDerectiveMouseoverFn__ = null;
    el.__vueDerectiveMouseleaveFn__ = null;
  },
};

export const vClickOutside = {
  // 初始化指令
  bind(el, binding, vnode) {
    function documentHandler(e) {
      // 这里判断点击的元素是否是本身，是本身，则返回
      if (el.contains(e.target)) {
        return false;
      }
      // 判断指令中是否绑定了函数
      if (binding.expression) {
        // 如果绑定了函数 则调用那个函数，此处binding.value就是handleClose方法
        binding.value(e);
      }
    }
    // 给当前元素绑定个私有变量，方便在unbind中可以解除事件监听
    el.__vueClickOutside__ = documentHandler;
    document.addEventListener("click", documentHandler);
  },
  update() {},
  unbind(el, binding) {
    // 解除事件监听
    document.removeEventListener("click", el.__vueClickOutside__);
    el.__vueClickOutside__ = null;
  },
};

export default (Vue) => {
  Vue.directive("resize", vResize);
  Vue.directive("mouseHover", vMouseHover);
  Vue.directive("clickOutside", vClickOutside);
};
