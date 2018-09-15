var app = new Vue({
  el: "#container",
  data: {
    user: "home",
    types: [],
    facilities: [],
    aWorkerName: "",
    aWorkerShift: ""
  },
  mounted() {
    this.adminFiller();
  },
  methods: {
    adminFiller: () => {
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

      fetch("api/certification")
        .then(res => res.json())
        .then(data => {
          this.certificates = data;
        })
        .catch(err => console.error(err));
    },

    addNewWorker: () => {
      fetch("/api/worker", {
        method: "POST",
        body: {
          name: this.aWorkerName,
          shift: this.aWorkerShift
        }
      })
        .then(res => res.json())
        .then(data => {
          this.aWorkerName = "";
          this.aWorkerShift = "";
        })
        .catch(err => console.error(err));
    }
  }
});
