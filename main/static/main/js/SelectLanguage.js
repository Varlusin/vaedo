class SelectLanguage {
  selector = {
    rot: "[data-js-lenguage]",
    lnBnt: "[data-js-lenguage-button]",
    lnMenu: "[data-js-lenguage-menu]",
  };

  stateClasses = {
    isShow: "is-show",
    isLock: "is-lock",
  };

  lenguageList = [
    {
      lnCode: "hy",
      lnValue: "ՀՅ",
      imgUrl: "/static/main/img/Arm_flag.svg",
    },
    {
      lnCode: "ru",
      lnValue: "РУ",
      imgUrl: "/static/main/img/rus_flag.svg",
    },
    {
      lnCode: "en",
      lnValue: "EN",
      imgUrl: "/static/main/img/us_flag.svg",
    },
  ];
  constructor() {
    this.rotElement = document.querySelector(this.selector.rot);
    this.butonElement = this.rotElement.querySelector(this.selector.lnBnt);
    this.menuElement = this.rotElement.querySelector(this.selector.lnMenu);
    this.currentLanguage = this.getCookie("language");
    this.lenguageList.forEach((value) => {
      if (this.currentLanguage === value.lnCode) {
        this.butonElement.innerHTML = value.lnValue;
      } else {
        let li = document.createElement("li");
        li.className = "flex_box head_li ln_menu__li";
        li.innerHTML += `<img src="${value.imgUrl}" alt=""><h3>${value.lnValue}</h3>`;
        li.addEventListener("click", () => {
          this.fetchChangeLanguage(value.lnCode)
          // this.menuElement.classList.remove(this.stateClasses.isShow);
        });
        this.menuElement.append(li);
      }
    });

    this.bindEvent();
  }

  getLenguageFromUrl = () => {
    const pathSegments = window.location.pathname.split("/").filter(Boolean);
    return pathSegments.length > 0 ? pathSegments[0] : null;
  };

  lnButtonClick = () => {
    this.menuElement.classList.toggle(this.stateClasses.isShow);
  };

  bindEvent() {
    this.butonElement.addEventListener("click", this.lnButtonClick);
  }

  getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
  }

  fetchChangeLanguage(lnCode){
    fetch(`/set-language?lang=${lnCode}`).then(()=> window.location.reload())
  }

}

export { SelectLanguage };
