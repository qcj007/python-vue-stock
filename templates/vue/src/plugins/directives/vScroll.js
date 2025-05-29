import _ from "lodash-es";

function onScrollFun(el, binding) {
  const { onScrollBottom, onScroll } = binding.value || {};
  const scrollTop = Math.round(el.scrollTop);
  const clientHeight = el.clientHeight;
  const scrollHeight = el.scrollHeight;
  onScroll && onScroll({ scrollTop, clientHeight, scrollHeight });
  if (scrollTop + clientHeight >= scrollHeight) {
    onScrollBottom && onScrollBottom();
  }
}

export const vScroll = {
  mounted(el, binding) {
    el.__vueEventScroll__ = _.throttle(onScrollFun(el, binding), 100);
    el.addEventListener("scroll", el.__vueEventScroll__, true);
  },
  unmounted(el) {
    el.removeEventListener("scroll", el.__vueEventScroll__, true);
    el.__vueEventScroll__ = null;
    el = null;
  }
};

export default vScroll;
