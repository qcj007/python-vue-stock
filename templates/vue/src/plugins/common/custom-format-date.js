import moment from "moment";
/**
 * 毫秒转换
 * @param milliseconds 毫秒
 * @returns 00：00：00：00
 */
function millisecondsToFullStr(milliseconds) {
  let $moment = moment.duration(milliseconds, "milliseconds");
  return [
    $moment
      .hours()
      .toString()
      .padStart(2, "0"),
    $moment
      .minutes()
      .toString()
      .padStart(2, "0"),
    $moment
      .seconds()
      .toString()
      .padStart(2, "0"),
    parseInt($moment.milliseconds() / 40)
      .toString()
      .padStart(2, "0"),
  ].join(":");
}

/**
 * 毫秒转换
 * @param milliseconds 毫秒
 * @returns 00：00
 */
function millisecondsToSecondsStr(milliseconds) {
  let $moment = moment.duration(milliseconds, "milliseconds");
  return [
    $moment
      .minutes()
      .toString()
      .padStart(2, "0"),
    $moment
      .seconds()
      .toString()
      .padStart(2, "0"),
  ].join(":");
}

/**
 * 时间格式化
 * @param string 时间
 * @return 2020/02/01 12:21:21
 */
function formatTime(timeStr, format = "YYYY/MM/DD HH:mm:ss") {
  return moment(timeStr).format(format);
}

export { millisecondsToFullStr, millisecondsToSecondsStr, formatTime };
