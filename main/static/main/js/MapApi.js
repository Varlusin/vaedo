class RenderMapClas {
    rotMapElement = document.querySelector("[data-js-map]");
    mapDiv = this.rotMapElement.querySelector("[data-js-map-mapdiv]");
  
    STADYMAP = L.tileLayer(
      // "/static/main/img/tile/{z}/{x}/{y}.png",
      'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
      {
        // attribution: '<a http="https://yandex.ru" target="_blank">Yandex</a>',
        maxNativeZoom: 19,
      }
    );
  
    MAP_PARAMETER = {
      center: [40.785273, 43.841774],
      zoom: 13,
      attributionControl: false,
      minZoom: 12,
      maxZoom: 18,
      maxBounds: L.latLngBounds(
        L.latLng(40.854, 43.7603),
        L.latLng(40.705, 43.9263)
      ),
      zoomControl: false,
      layers: [this.STADYMAP],
    };
  
    constructor() {
      this.map = new L.map(this.mapDiv, this.MAP_PARAMETER);
      this.map.options.crs = L.CRS.EPSG3395;
      this.map.on("click", this.mapClickEvent);
  
      this.map.addControl(
        new this.CustomZoomControl({ position: "topleft", map: this.map })
      );
      this.map.addControl(
        new this.GPSControl({ position: "topright", addMarker: this.addMarker })
      );
    }
  
  
    fatchGetLocation = async (lat, lon) => {
      try {
        const responce = await fetch(
          `http://192.168.10.18:8000/hy/api/location/?latitude=${lat}&longitude=${lon}`,
          {
            headers: {
              Accept: "application.json",
              "X-Reguested-With": "XMLHttpRequest",
            },
          }
        );
    
        if (!responce.ok) {
          throw new Error(`HTTP eror: ${responce.status}`);
        }
        const newDataJson = await responce.json();
        console.log(newDataJson)
      } catch (error) {
        console.error(error.message);
      }
    };
  
  
  
    mapClickEvent = (event) => {
      this.fatchGetLocation(event.latlng.lng, event.latlng.lat)
      this.addMarker([event.latlng.lng, event.latlng.lat]);
    };
  
    addMarker = (data, anim = false) => {
      if (this.currentMarker) {
        this.map.removeLayer(this.currentMarker);
      }
  
      const greenIcon = L.icon({
        iconUrl: "/static/main/img/loc_icon.svg",
        iconSize: [38, 95],
        iconAnchor: [22, 94],
        popupAnchor: [-3, -76],
      });
      this.currentMarker = L.marker([...data].reverse(), {
        icon: greenIcon,
      }).addTo(this.map);
      if (anim) {
        this.map.flyTo([...data].reverse(), 18, {
          animate: true,
          duration: 2,
        });
      }
    };
  
    CustomZoomControl = L.Control.extend({
      onAdd: function () {
        const div = L.DomUtil.create("div", "custom-zoom-control");
  
        const zoomInButton = L.DomUtil.create("button", "", div);
        zoomInButton.innerHTML = `<img src="/static/main/img/plus.svg" alt="" width="25" height="25">`;
        zoomInButton.onclick = () => this.options.map.zoomIn();
  
        const zoomOutButton = L.DomUtil.create("button", "", div);
        zoomOutButton.innerHTML = `<img src="/static/main/img/minus.svg" alt="" width="25" height="25">`;
        zoomOutButton.onclick = () => this.options.map.zoomOut();
  
        L.DomEvent.disableClickPropagation(div);
  
        return div;
      },
      initialize: function (options) {
        this.options = options;
      },
    });
  
    GPSControl = L.Control.extend({
      onAdd: function () {
        const div = L.DomUtil.create("div", "gps-control");
        const gpsButton = L.DomUtil.create("button", "", div);
        gpsButton.innerHTML = `<img src="/static/main/img/gps.svg" alt="" width="25" height="25">`;
  
        gpsButton.addEventListener("click", () => {
          if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((position) => {
              const { latitude, longitude } = position.coords;
              this.options.addMarker([longitude, latitude], true)
            });
          } else {
            alert("Geolocation is not supported by your browser.");
          }
        });
  
        L.DomEvent.disableClickPropagation(div);
        return div;
      },
      initialize: function (options) {
        this.options = options; 
      },
    });
  }
  
  class MapApi {
    selector = {
      closeMapBnt: "[data-js-map-close]",
  
      rot: "[data-js-location]",
      adresInput: "[data-js-location-input]",
      openMapBnt: "[data-js-location-buton]",
      adresMenu: "[data-js-location-menu]",
      srcIcon: "[data-js-location-srcicon]",
    };
  
    constructor() {
      this.RenderMap = new RenderMapClas();
  
      this.rotElement = document.querySelector(this.selector.rot);
      this.inputElement = this.rotElement.querySelector(this.selector.adresInput);
      this.menuElement = this.rotElement.querySelector(this.selector.adresMenu);
      this.bntElement = this.rotElement.querySelector(this.selector.openMapBnt);
  
      this.RenderMap.rotMapElement
        .querySelector(this.selector.closeMapBnt)
        .addEventListener("click", () => {
          this.RenderMap.rotMapElement.classList.remove("is-show");
        });
  
      this.localStorageOrderAdres();
      this.inputclickEvent();
      this.butonEvent();
      this.getOldLocation();
    }
  
    butonEvent() {
      this.bntElement.addEventListener("click", () => {
        this.RenderMap.rotMapElement.classList.add("is-show");
      });
    }
  
    inputclickEvent() {
      this.inputElement.addEventListener("click", () => {
        this.rotElement
          .querySelector(this.selector.srcIcon)
          .classList.add("is-show");
  
        this.menuElement.classList.add("is-show");
      });
    }
  
    localStorageOrderAdres = () => {
      let storageOrderAdres = localStorage.getItem("orderAdres");
      if (!storageOrderAdres) {
        return this.getOrderAdres();
      }
  
      storageOrderAdres = JSON.parse(storageOrderAdres);
  
      if (storageOrderAdres.properties) {
        this.renderLocation(storageOrderAdres);
      }
    };
  
    getOrderAdres = async () => {
      try {
        const responce = await fetch("./js/orderAdres.json");
        if (!responce.ok) {
          throw new Error(`not fond`);
        }
        const orderAdres = await responce.json();
        if (orderAdres.success) {
          this.renderLocation(orderAdres.orderAdres);
        }
        localStorage.setItem("orderAdres", JSON.stringify(orderAdres.orderAdres));
      } catch (error) {
        console.error(error.message);
      }
    };
  
    getOldLocation = async () => {
      try {
        const responce = await fetch("./js/oldloc.json");
        if (!responce.ok) {
          throw new Error("not fond");
        }
        const oldLoc = await responce.json();
        if (oldLoc.success) {
          this.renderOldLocation(oldLoc.old_location.features);
        }
      } catch (error) {
        console.error(error.message);
      }
    };
  
    renderOldLocation = (data) => {
      let ul = document.createElement("ul");
      ul.className = "search_rezult-menu";
      data.forEach((value) => {
        let li = document.createElement("li");
        li.className = "flex_box head_li search_rezult";
        li.innerHTML = `<img class="svg-img" src="/static/main/img/old_loc_icon.svg" alt="" width="25" height="25">
                        <P>${value.properties.adres}</P>`;
  
        li.addEventListener("click", () => {
          this.menuElement.classList.remove("is-show");
          this.renderLocation(value);
          localStorage.setItem("orderAdres", JSON.stringify(value));
        });
        ul.append(li);
      });
      this.menuElement.append(ul);
    };
  
    renderLocation = (data) => {
      this.inputElement.value = data.properties.adres;
      this.RenderMap.addMarker(data.geometry.coordinates, true);
    };
  }
  
  export { MapApi };
  
