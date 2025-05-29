
import { ref } from 'vue'
const elid = ref(null)
const callBackFun = ref()
const handlerClick = (event) => {
  if (elid.value) {
    let isSelf = elid.value.contains(event.target)  // 这个是自己的区域
    if (!isSelf) {
      // console.log('没在区域里面-->>>')
      callBackFun.value()
    } else {
      // console.log('在区域里--->>>>>')
    }
  }
}


const vContains = {
  mounted(el, binding) {
    // el为绑定的元素，binding为绑定给指令的对象
    const { callBack } = binding.value
    elid.value = el
    callBackFun.value = callBack
    document.addEventListener('click', handlerClick)  // 监听 document 点击事件
  },
  unmounted(el) {
    document.removeEventListener('click', handlerClick)
  },
}

export default vContains

