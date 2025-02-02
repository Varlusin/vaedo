"use strict";

import { SelectLanguage } from "./SelectLanguage.js";
import { ProfileMenu } from "./ProfileMenu.js";
import { MapApi } from "./MapApi.js";

window.addEventListener("load", () => {
  new SelectLanguage();
  new ProfileMenu();
  new MapApi();
});

