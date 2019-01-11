<template>
  <div class="o-time-date">
    <div>
      <span v-if="days != 'TBD'">
        <v-chip  v-for="(char, index) in days" :key="index" d-inline-flex>
          {{ char }}
        </v-chip>
      </span>
      <v-chip v-else d-inline-flex>TBD</v-chip>
    </div>
    <div>
      <span v-if="times && times.length > 0">
        <v-chip v-for="(time, index) in times" :key="index" d-inline-flex>
          {{ time }}
        </v-chip>
      </span>
      <v-chip v-else d-inline-flex>TBD</v-chip>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TimeDateDisplay',
  props: {
    times: {
      type: Array,
      required: false,
    },
    days: {
      type: String,
      required: false,
    },
  },
};
</script>

<style>

</style>
