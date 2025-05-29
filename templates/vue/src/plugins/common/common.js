import html2canvas from "html2canvas";
/**
 * 函数节流
 */
function throttle(fn, delay = 500) {
  let startTime = 0;
  return (...args) => {
    let timeNow = +new Date();
    if (timeNow - startTime >= delay) {
      fn(...args);
      startTime = timeNow;
    }
  };
}

/**
 * 函数防抖
 */
function debounce(fn, delay = 500) {
  let timer = null;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      fn(...args);
    }, delay);
  };
}

/**
 * @description: 递归数据修改value
 * @param {any} value
 * @param {fuction} fn
 * @param {string} type
 * @return {any}
 */
function deepRecursionSpecailValue(value, fn, type) {
  const valueType = typeof value;
  if (valueType === "object" && valueType !== null) {
    if (Array.isArray(value)) {
      value = value.map((item) => deepRecursionSpecailValue(item, fn, type));
    } else {
      for (let key in value) {
        value[key] = deepRecursionSpecailValue(value[key], fn, type);
      }
    }
  } else {
    if (!type || type === valueType) {
      value = fn.call(null, value);
    }
  }
  return value;
}

function asyncSetTimeout(fn, par, timeout = 2000) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve(fn(par));
    }, timeout);
  });
}

function isLineIntersecy(lineA, LineB) {
  const { start: startX1, end: endX1 } = lineA;
  const { start: startX2, end: endX2 } = LineB;

  if (startX1 < startX2 && endX1 >= startX2) return true;
  if (startX1 >= startX2 && startX1 <= endX2) return true;

  return false;
}

function isRectIntersect(rectA, rectB) {
  const { x: x1, y: y1, width: w1, height: h1 } = rectA;
  const { x: x2, y: y2, width: w2, height: h2 } = rectB;

  const isIntersectX = isLineIntersecy({ start: x1, end: x1 + w1 }, { start: x2, end: x2 + w2 });
  const isIntersectY = isLineIntersecy({ start: y1, end: y1 + h1 }, { start: y2, end: y2 + h2 });

  return isIntersectX && isIntersectY;
}

function getRandomString(len) {
  len = len || 32;
  var chars = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678";
  var maxPos = chars.length;
  var pwd = "";
  for (let i = 0; i < len; i++) {
    pwd += chars.charAt(Math.floor(Math.random() * maxPos));
  }
  return pwd;
}

/**
 * @description: 复制到剪切板
 * @param {string} text
 * @return {*}
 */
function onClipboard(text) {
  const input = document.createElement("input");
  document.body.appendChild(input);
  input.setAttribute("value", text);
  input.select();
  if (document.execCommand("copy")) {
    document.execCommand("copy");
    document.body.removeChild(input);
    return true;
  }
  document.body.removeChild(input);
  return false;
}

/**
 * @description: 获取高亮正则
 * @param {array} keys
 * @return {RegExp}
 */
function getHeightLightReg(keys = []) {
  return new RegExp(`${keys.map((key) => `(${key})`).join("|")}`, "g");
}

/**
 * @description: 替换高亮内容
 * @param {array} keys 关键词
 * @param {string} text 内容
 * @param {function | string} handler 替换处理
 * @return {string} 替换后内容
 */
function replaceHeightLight(keys = [], text = "", handler) {
  return text.replace(getHeightLightReg(keys), handler);
}

/**
 * 将以base64的图片url数据转换为Blob
 * @param urlData
 * 用url方式表示的base64图片数据
 */
function convertBase64UrlToBlob(urlData) {
  const bytes = window.atob(urlData.split(",")[1]); //去掉url的头，并转换为byte
  //处理异常,将ascii码小于0的转换为大于0
  const ab = new ArrayBuffer(bytes.length);
  let ia = new Uint8Array(ab);
  for (let i = 0; i < bytes.length; i++) {
    ia[i] = bytes.charCodeAt(i);
  }
  return new Blob([ab], { type: "image/png" });
}

/**
 * @description: 将dom元素转为base64格式的图片
 * @param {HTMLElement} el dom元素
 * @return {string} 图片base64码
 */
async function htmlElementToBase64Image(el) {
  if (el) {
    console.log("el", el);
    const canvas = await html2canvas(el, {
      useCORS: true, // 【重要】开启跨域配置
      scale: window.devicePixelRatio < 3 ? window.devicePixelRatio : 2,
      allowTaint: true, // 允许跨域图片
      logging: false
    });
    return canvas.toDataURL("image/jpeg", 1.0);
  }
  return "";
}



export {
  throttle,
  debounce,
  deepRecursionSpecailValue,
  asyncSetTimeout,
  isLineIntersecy,
  isRectIntersect,
  getRandomString,
  onClipboard,
  getHeightLightReg,
  replaceHeightLight,
  convertBase64UrlToBlob,
  htmlElementToBase64Image,
};
