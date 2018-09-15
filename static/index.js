var app = new Vue({
  el: "#container",
  data: {
    user: "home",

    types: [],

    facilities: [],

    aLongitude: "",
    aLatitude: "",

    aWorkerName: "",
    aWorkerShift: "",

    aNewEquipmentType: "",

    probabilityFailure: "",
    hourMin: "",
    hourMax: "",
    equipmentTypeId: "",
    facilityId: ""
  },
  mounted() {
    this.adminFiller();
  },
  methods: {
    //get equipmentType and list of facilities number
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
        });
    },

    //add new equipment type
    addNewEquipmentType: function() {
      fetch("/api/equipment_type", {
        method: "post",
        body: JSON.stringify({
          name: this.aNewEquipmentType
        }),
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(res => res.json())
        .then(data => {
          this.aNewEquipmentType = "";
        });
    },

    //add new equipment details
    addNewEquipment: function() {
      fetch("/api/equipment", {
        method: "post",
        body: JSON.stringify({
          prob: this.probabilityFailure,
          hour_min:this.hourMin,
          hour_max:this.hourMax,
          equipment_id_type:equipmentTypeId,
          facility_id:facility_id
        }),
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(res => res.json())
        .then(data => {
          this.probabilityFailure = "";
          this.hourMax="";
          this.hourMin="";
          this.equipmentTypeId="";
          this.facilityId="";
        });
    }
  }
});
