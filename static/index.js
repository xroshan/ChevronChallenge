var app = new Vue({
  el: "#container",

  data: {
    user: "home",

    showProfile: false,
    aViewProfile: "",

    workerNameForOrder: "",

    types: [],

    facilities: [],

    workers: [],

    equipments: [],

    allProfile: [],

    allEquipments: [],

    allOrders: [],

    positionCertificate: "",

    aLongitude: "",
    aLatitude: "",

    aWorkerName: "",
    aWorkerShift: "",

    aNewEquipmentType: "",

    probabilityFailure: "",
    hourMin: "",
    hourMax: "",
    aSelectedEquipment: "",
    aSelectedFacility: "",

    cPriorityId: "",
    cCompleteTime: "",
    cSelectedFacility: "",
    cSelectedEquipment: "",
    cSelectedWorker: "",
    cDate: ""
  },
  mounted() {
    this.adminFiller();
    this.clientFiller();
    this.getAllOrders();
    this.fillOrdersWithName();
  },
  methods: {
    //update admin page
    adminFiller: function() {
      fetch("/api/equipment_type")
        .then(res => res.json())
        .then(data => {
          this.types = data;
        })
        .catch(err => console.error(err));

      fetch("api/facility")
        .then(res => res.json())
        .then(data => {
          this.facilities = data;
        })
        .catch(err => console.error(err));
    },

    //update client page
    clientFiller: function() {
      fetch("api/worker")
        .then(res => res.json())
        .then(data => {
          this.workers = data;
        })
        .catch(err => console.error(err));

      fetch("/api/equipment")
        .then(res => res.json())
        .then(data => {
          this.equipments = data;
        })
        .catch(err => console.error(err));
    },

    //get all profile details
    getProfile: function() {
      fetch(`/api/worker/${this.aViewProfile}`)
        .then(res => res.json())
        .then(data => {
          console.log(data);
          this.allProfile = data;
        })
        .catch(err => console.error(err));
    },

    //get details of all available orders
    getAllOrders: function() {
      fetch(`/api/order`)
        .then(res => res.json())
        .then(data => {
          console.log(data);
          this.allOrders = data;
        })
        .catch(err => console.error(err));
    },

    fillOrdersWithName: function() {
      allOrders.forEach((e, i) => {
        fetch(`/api/order/${i}`)
          .then(res => res.json())
          .then(data => {
            this.allOrders[i] = data;
          })
          .catch(err => console.error(err));
      });
    },

    getEquipmentByFacility: function() {
      fetch(`/api/facility/${this.cSelectedFacility}`)
        .then(res => res.json())
        .then(data => {
          console.log(data);
          this.allEquipments = data;
        })
        .catch(err => console.error(err));
    },

    //add new worker's name and shift
    addNewWorker: function() {
      fetch("/api/worker", {
        method: "post",
        body: JSON.stringify({
          name: this.aWorkerName,
          shift: this.aWorkerShift
        }),
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(res => res.json())
        .then(data => {
          this.aWorkerName = "";
          this.aWorkerShift = "";
          this.clientFiller();
        })
        .catch(err => console.error(err));
    },

    //add facility latitude and longitude
    addNewFacility: function() {
      fetch("/api/facility", {
        method: "post",
        body: JSON.stringify({
          lat: this.aLongitude,
          lon: this.aLatitude
        }),
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(res => res.json())
        .then(data => {
          this.aLatitude = "";
          this.aLongitude = "";
          this.adminFiller();
        });
    },

    //add new equipment type
    addNewEquipmentType: function() {
      fetch("/api/equipment_type", {
        method: "post",
        body: JSON.stringify({
          name: this.aNewEquipmentType,
          prob: this.probabilityFailure,
          hour_min: this.hourMin,
          hour_max: this.hourMax
        }),
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(res => res.json())
        .then(data => {
          this.aNewEquipmentType = "";
          this.probabilityFailure = "";
          this.hourMin = "";
          this.hourMax = "";
          this.adminFiller();
        });
    },

    //add new equipment details
    addNewEquipment: function() {
      fetch("/api/equipment", {
        method: "post",
        body: JSON.stringify({
          equipment_type_id: this.aSelectedEquipment,
          facility_id: this.aSelectedFacility
        }),
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(res => res.json())
        .then(data => {
          this.aSelectedEquipment = "";
          this.aSelectedFacility = "";
          this.adminFiller();
        });
    },

    //submit order form
    submitOrderForm: function() {
      console.log(this.cSelectedEquipment);
      fetch("/api/order", {
        method: "post",
        body: JSON.stringify({
          priority: parseInt(this.cPriorityId),
          time_to_completion: parseInt(this.cCompleteTime),
          facility_id: this.cSelectedFacility,
          equipment_id: this.cSelectedEquipment
        }),
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(res => res.json())
        .then(data => {
          this.cPriorityId = "";
          this.cCompleteTime = "";
          this.cSelectedFacility = "";
          this.cSelectedEquipment = "";
          this.clientFiller();
        });
    },

    //add new certificate to a worker
    addNewCertificate: function() {
      fetch("/api/certification", {
        method: "post",
        body: JSON.stringify({
          equipment_type_id: this.aCertificateWorker,
          worker_id: this.aCertificateWorkerName
        }),
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(res => res.json())
        .then(data => {
          this.aCertificateWorker = "";
          this.aCertificateWorkerName = "";
          this.clientFiller();
        });
    }
  }
});
