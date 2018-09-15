var app = new Vue({
  el: "#container",
  data: {
    user: "home",

    types: [],

    facilities: [],

    workers: [],

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

    cPriorityId:"",
    cCompleteTime:"",
    cSelectedFacility:"",
    cSelectedEquipment:"",
    cSelectedWorker:""

  },
  mounted() {
    this.adminFiller();
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
    clientFiller: function(){
      fetch("api/worker")
        .then(res => res.json())
        .then(data => {
          this.workers = data;
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
          name: this.aNewEquipmentType
        }),
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(res => res.json())
        .then(data => {
          this.aNewEquipmentType = "";
          this.adminFiller();
        });
    },

    //add new equipment details
    addNewEquipment: function() {
      fetch("/api/equipment", {
        method: "post",
        body: JSON.stringify({
          prob: this.probabilityFailure,
          hour_min: this.hourMin,
          hour_max: this.hourMax,
          equipment_type_id: this.aSelectedEquipment,
          facility_id: this.aSelectedFacility
        }),
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(res => res.json())
        .then(data => {
          this.probabilityFailure = "";
          this.hourMax = "";
          this.hourMin = "";
          this.aSelectedEquipment = "";
          this.aSelectedFacility = "";
          this.adminFiller();
        });
    },

    //submit order form
    submitOrderForm: function(){
      fetch("/api/order",{
        method:"post",
        body:JSON.stringify({
          priority:this.cPriorityId,
          time_to_completion:this.cCompleteTime,
          facility_id:this.cSelectedFacility,
          equipment_id:this.cSelectedEquipment,
          worker_id:this.cSelectedWorker
        }),
        headers: {
          "Content-Type": "application/json"
        }
      })
      .then(res => res.json())
      .then(data => {
        this.cPriorityId= "";
        this.cCompleteTime = "";
        this.cSelectedFacility = "";
        this.cSelectedEquipment = "";
        this.cSelectedWorker = "";
        this.clientFiller();
      });
    }
  }
});
