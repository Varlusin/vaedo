class Futur {
  constructor() {
    this.rotElement = document.querySelector("[data-js-futur]");
    this.getFutur();
  }

  renderFutur(responce) {
    responce.forEach((value) => {
      let footerColumn = document.createElement("div");
      footerColumn.className = "footer-column";
      footerColumn.innerHTML += `<div class="column-title" >${value.futurtype}</div>`;
      value.futur.forEach((futur) => {
        footerColumn.innerHTML += `<a href="${futur.url}" class="footer-column-link">${futur.names}</a>`;
      });
      this.rotElement.before(footerColumn);
    });
  }

  getFutur = async () => {
    try {
      const responce = await fetch(`/futur/?format=json`);
      if (!responce.ok) {
        throw new Error("not fond");
      }
      const futurData = await responce.json();
      this.renderFutur(futurData);
    } catch (error) {
      console.error(error.message);
    }
  };
}
export { Futur };
