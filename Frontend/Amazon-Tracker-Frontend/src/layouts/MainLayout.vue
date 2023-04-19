<template>
  <div class="container-column">
    <div class="row-item-1">
      <p style="font-size: 3em"> Login to get Trackin !!</p>
    </div>
    <div class="row-item-2" style="padding-bottom: 50px">
      <q-btn to="/sign-in" style="font-size: 1.5em; margin-bottom: 40px; width: 250px" outline rounded color="green" label="Login"/>
      <q-separator ></q-separator>
    </div>
    <div class="row-item-3">
      <q-timeline :layout="layout" color="secondary">
        <q-timeline-entry heading>
          Features
          <br>
        </q-timeline-entry>

        <q-timeline-entry
          title="Tracking"
          side="left"
          icon="analytics"
          color="red"
        >
          <div>
            Simple and use to get started. Copy the link for the product you want to track.
          </div>
        </q-timeline-entry>

        <q-timeline-entry
          title="Toggle Notification"
          side="right"
          color="blue"
          icon="notifications"
        >
          <div>
            Enable and disable the notification service to have fine grain control over the tracking.
          </div>
        </q-timeline-entry>

        <q-timeline-entry
          title="Types of Notifications"
          side="left"
          color="green"
          icon="format_list_bulleted"
        >
          <div>
            Select between getting notified every 12 hours or when the product price drops.
          </div>
        </q-timeline-entry>

        <q-timeline-entry heading>Enjoy</q-timeline-entry>


      </q-timeline>
    </div>
  </div>
</template>

<script>
import {defineComponent, ref} from "vue";
import {computed} from 'vue'
import {useQuasar} from "quasar";

export default defineComponent({
  name: "MainLayout",
  components: {},
  setup() {
    const $q = useQuasar();

    return {
      standard: ref(2),
      min: ref(),
      max: ref(),
      val: ref(0),
      layout: computed(() => {
        return $q.screen.lt.sm ? 'dense' : ($q.screen.lt.md ? 'comfortable' : 'loose')
      })
    };
  }
});
</script>

<style scoped>
.container-column {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
