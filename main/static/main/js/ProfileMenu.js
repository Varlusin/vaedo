import { RenderProfileForm } from "./RenderProfileForm.js";





class ProfileMenu {
    selector = {
      rot: "[data-js-profile]",
      profileBnt: "[data-js-profile-button]",
      profileMenu: "[data-js-profile-menu]",
    };
  
    stateClasses = {
      isShow: "is-show",
      isLock: "is-lock",
    };
  
    menuList = {
      dontAuth: [
        {
          profilType: "login",
          url: "/api/token/",
          Value: "Մուտք",
          imgUrl: "/static/main/img/login.svg",
        },
        {
          profilType: "registration",
          url: "/rg/",
          Value: "Գրանցվել",
          imgUrl: "/static/main/img/registration.svg",
        },
      ],
      auth: [
        {
          profilType: "user",
          url: "#",
          Value: "Փոփոխել",
          imgUrl: "/static/main/img/change_profile.svg",
        },
        {
          profilType: "user",
          url: "#",
          Value: "Դուրս գալ",
          imgUrl: "/static/main/img/logout.svg",
        },
      ],
    };
  
    constructor() {
      this.rotElement = document.querySelector(this.selector.rot);
      this.butonElement = this.rotElement.querySelector(this.selector.profileBnt);
      this.menuElement = this.rotElement.querySelector(this.selector.profileMenu);
      this.renderProfileMenu();
  
      this.bindEvent();
    }
  
    renderProfileMenu() {
      this.autentication
        ? this.ProfileMenuComponents("auth")
        : this.ProfileMenuComponents("dontAuth");
    }
  
    ProfileMenuComponents = (auth) => {
      this.menuList[auth].forEach((value) => {
        let li = document.createElement("li");
        li.addEventListener("click", () => {new RenderProfileForm(value.url, value.profilType)});
        li.innerHTML += `<div class="flex_box head_li ln_menu__li">
                            <img class="svg-img" src="${value.imgUrl}" alt="" width="25" height="25">
                              <p>${value.Value}</p>
                          </div>`;
        this.menuElement.append(li);
      });
    };
  
    profButtonClick = () => {
      this.menuElement.classList.toggle(this.stateClasses.isShow);
    };
  
    bindEvent() {
      this.butonElement.addEventListener("click", this.profButtonClick);
    }
  }
  
  export { ProfileMenu };
  