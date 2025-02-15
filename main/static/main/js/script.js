"use strict";

import { SelectLanguage } from "./SelectLanguage.js";
import { ProfileMenu } from "./ProfileMenu.js";
import { MapApi } from "./MapApi.js";
import { Futur } from "./Futur.js";

window.addEventListener("load", () => {
  const lenguage = new SelectLanguage();
  const lnCode = lenguage.getLenguageFromUrl()
  new ProfileMenu();
  new MapApi();
  new Futur(lnCode);
});
