import vResize from "./vResize";
import vMouseHover from "./vMouseHover";
import vContains from "./vContains";
import vScroll from "./vScroll";
import vClickOutside from "./vClickOutside";

export default {
  install(app) {
    app.directive("resize", vResize);
    app.directive("hover", vMouseHover);
    app.directive("contains", vContains);
    app.directive("scroll", vScroll);
    app.directive("clickOutside", vClickOutside);
  }
};
