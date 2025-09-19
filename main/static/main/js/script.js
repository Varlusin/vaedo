"use strict";

import { SelectLanguage } from "./SelectLanguage.js";
import { ProfileMenu } from "./ProfileMenu.js";
import { MapApi } from "./MapApi.js";
import { Futur } from "./Futur.js";

window.addEventListener("load", () => {
  new SelectLanguage();
  new ProfileMenu();
  new MapApi();
  new Futur();
});
