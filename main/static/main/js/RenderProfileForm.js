class RenderProfileForm {
  constructor(url, profileType) {
    this.url = url;
    this.profileType = profileType;
    this.rootElement = document.querySelector("[data-js-registerroot]");
    this.renderRoot();
    this.form = this.renderForm();
    this.init();
    this.rootElement.classList.add("is-show");
  }

  renderRoot() {
    this.rootElement.innerHTML = `
      <div style="height: 100%">
        <div class="map_container">
          <button class="close-map" data-js-registerclose>
            <img src="/static/main/img/close.svg" alt="Close" />
          </button>
          <div class="map" data-js-form></div>
        </div>
      </div>`;
    this.rootElement
      .querySelector("[data-js-registerclose]")
      .addEventListener("click", () => {
        this.rootElement.classList.remove("is-show");
      });
  }

  renderForm() {
    const isLogin = this.profileType === "login";
    const formFields = isLogin
      ? `
        ${this.renderInputHTML("username", "text", "Имя пользователя", true)}
        ${this.renderPasswordHTML(1)}
      `
      : `
        ${this.renderInputHTML("username", "text", "Имя пользователя", true)}
        ${this.renderPasswordHTML(2)}
        ${this.renderInputHTML("email", "email", "Email", true)}
        ${this.renderInputHTML("first_name", "text", "Имя", true)}
        ${this.renderInputHTML("last_name", "text", "Фамилия", true)}
        ${this.renderInputHTML("phone", "text", "Телефон", true)}
      `;

    this.rootElement.querySelector("[data-js-form]").innerHTML = `
      <div class="profile-form">
        <div class="profile-form__header">
          <h2 class="profile-form__title">${this.profileType}</h2>
        </div>
        <form class="profile-form__form" action="javascript:alert('Hello there, I am being submitted');">
          ${formFields}
          <button type="submit" class="register-button">Зарегистрироваться</button>
        </form>
      </div>`;
    const form = this.rootElement.querySelector(".profile-form__form");
    this.addPasswordToggleListeners(form);
    return form;
  }

  renderInputHTML(name, type, placeholder, required) {
    return `<input type="${type}" name="${name}" placeholder="${placeholder}" ${
      required ? "required" : ""
    }>`;
  }

  renderPasswordHTML(count) {
    let html = "";
    for (let i = 0; i < count; i++) {
      html += `
        <div class="password-field">
          <input type="password" name="password${i + 1}" placeholder="Пароль ${
        i + 1
      }" required>
          <button type="button" class="toggle-password" data-target="password${
            i + 1
          }">👁</button>
        </div>`;
    }
    return html;
  }

  addPasswordToggleListeners(form) {
    form.querySelectorAll(".toggle-password").forEach((button) => {
      button.addEventListener("click", () => {
        const targetInput = form.querySelector(
          `input[name='${button.dataset.target}']`
        );
        targetInput.type = targetInput.type === "password" ? "text" : "password";
        button.textContent = targetInput.type === "password" ? "👁" : "🙈";
      });
    });
  }

  handleBackendErrors(errors) {
    // Clear previous errors
    this.form.querySelectorAll(".error").forEach((field) => {
      field.classList.remove("error");
      field.setCustomValidity("");
    });

    // Display new errors
    Object.keys(errors).forEach((fieldName) => {
      const field = this.form.querySelector(`[name="${fieldName}"]`);
      if (field) {
        const errorMessage = errors[fieldName][0];
        field.classList.add("error");
        field.setCustomValidity(errorMessage);
        field.reportValidity();
      }
    });
  }


  ferchProfile = async (url = this.url) => {
    try {

      const formData = new FormData(this.form);
      const data = Object.fromEntries(formData.entries());
      console.log(data);


      const responce = await fetch(url);
      if (!responce.ok) {
        throw new Error(`not fond`);
      }
      const orderAdres = await responce.json();
      if (orderAdres.success) {
        // this.renderLocation(orderAdres.orderAdres);
      }
      localStorage.setItem("orderAdres", JSON.stringify(orderAdres.orderAdres));
    } catch (error) {
      console.error(error.message);
    }
  };






  init() {
    this.form.addEventListener("submit", (event) => {

      this.ferchProfile();
      // event.preventDefault();

  //     const formData = new FormData(this.form);
  //     const data = Object.fromEntries(formData.entries());

  //     fetch(this.url, {
  //       method: "POST",
  //       body: JSON.stringify(data),
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //     })
  //       .then((response) => {
  //         if (!response.ok) {
  //           return response.json().then((errors) => {
  //             this.handleBackendErrors(errors);
  //           });
  //         }
  //         return response.json();
  //       })
  //       .then((data) => {
  //         console.log("Success:", data);
  //         this.rootElement.classList.remove("is-show");
  //       })
  //       .catch((error) => {
  //         console.error("Error:", error);
  //       });
    });
  }
}

export { RenderProfileForm };