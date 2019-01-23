<template>
  <div class="c-time-date">
    <v-chip>{{ days }}</v-chip>
    <v-chip v-if="times && times.length > 0">
      {{ times[0] }} to {{ times[1] }}
    </v-chip>
    <v-chip v-else d-inline-flex>TBD</v-chip>
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
.c-time-date {
  display: inline-flex;
}
</style>
