<template>
  <v-card class="text-xs-center">
    <v-chip>{{ item.course.sc }} {{ item.course.cn }}-{{ item.sec }}</v-chip>
    <v-chip>Credits: {{ item.course.cr }}</v-chip>
    <v-chip>Instructor: {{ item.instructor }} </v-chip>
    <v-chip>{{ item.course.it }} </v-chip>
    <v-chip>{{ item.course.im }}</v-chip>
  </v-card>
</template>

<script>
/* webpackChunkName: "v-card" */
const VCard = () => import('vuetify/es5/components/VCard/VCard');
/* webpackChunkName: "v-chip" */
const VChip = () => import('vuetify/es5/components/VChip/VChip');

export default {
  name: 'ClassListingSelected',
  components: {
    VCard,
    VChip,
  },
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style>

</style>
