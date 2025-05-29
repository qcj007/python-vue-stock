import { isEqual } from "lodash-es";

export default {
  // 更新数据
  setData(state, payload = {}) {
    for (let key in payload) {
      const tempVal = Reflect.get(payload, key);
      if (Reflect.has(state, key) && !isEqual(Reflect.get(state, key), tempVal)) {
        Reflect.set(state, key, tempVal);
      }
    }
  },
 
};
