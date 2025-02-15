class Futur {
  constructor(lnCode) {
    this.lnCode = lnCode;
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
      this.rotElement.append(footerColumn);
    });
  }

  getFutur = async () => {
    try {
      const responce = await fetch(`/${this.lnCode}/futur/?format=json`);
      if (!responce.ok) {
        throw new Error("not fond");
      }
      const oldLoc = await responce.json();
      this.renderFutur(oldLoc);
    } catch (error) {
      console.error(error.message);
    }
  };
}
export { Futur };
