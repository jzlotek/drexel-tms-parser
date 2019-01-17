<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="items"
      :loading="isLoading"
      class="elevation-1 text-s-left"
    >
      <v-progress-linear slot="progress" color="secondary" indeterminate/>
      <template slot="no-data">
        <v-alert v-if="loadedOnce" :value="true" color="error">
          Sorry, no classes found :(
        </v-alert>
      </template>
      <template slot="items" slot-scope="props">
        <ClassListingRow :props="props"/>
      </template>
    </v-data-table>
    <v-btn @click="loadListing()">Reload</v-btn>
    <v-expansion-panel>
      <v-expansion-panel-content
        v-for="(item, index) in selected"
        :key="index"
      >
        <div slot="header">
          <v-btn fab small @click="removeFromSelected(index)">
            <v-icon>remove_circle</v-icon>
          </v-btn>
          {{ item.course.title }}&nbsp;
          <v-chip>{{ item.course.sc }} {{ item.course.cn }}-{{ item.sec }}</v-chip>&nbsp;
          <v-btn :href="item.crnLink" target="_blank">{{ item.crn }}</v-btn>
        </div>
        <ClassListingSelected
        :item="item"/>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </div>
</template>

<script>
import EventBus from '../EventBus';
import { UPDATE_CLASSES, REMOVE_FROM_SELCTED } from '../store/constants';
/* webpackChunkName: "class-listing-row" */
const ClassListingRow = () => import('./ClassListingRow');
/* webpackChunkName: "class-listing-selected" */
const ClassListingSelected = () => import('./ClassListingSelected');
/* webpackChunkName: "v-data-table" */
const VDataTable = () => import('vuetify/es5/components/VDataTable/VDataTable');
/* webpackChunkName: "v-progress-linear" */
const VProgressLinear = () => import('vuetify/es5/components/VProgressLinear/VProgressLinear');
/* webpackChunkName: "v-alert" */
const VAlert = () => import('vuetify/es5/components/VAlert/VAlert');
/* webpackChunkName: "v-icon" */
const VIcon = () => import('vuetify/es5/components/VIcon/VIcon');
/* webpackChunkName: "v-btn" */
const VBtn = () => import('vuetify/es5/components/VBtn/VBtn');
/* webpackChunkName: "v-expansion-panel" */
const VExpansionPanel = () => import('vuetify/es5/components/VExpansionPanel/VExpansionPanel');
/* webpackChunkName: "v-expansion-panel-content" */
const VExpansionPanelContent = () => import('vuetify/es5/components/VExpansionPanel/VExpansionPanelContent');
/* webpackChunkName: "v-chip" */
const VChip = () => import('vuetify/es5/components/VChip/VChip');

export default {
  name: 'ClassListing',
  components: {
    ClassListingRow,
    ClassListingSelected,
    VDataTable,
    VProgressLinear,
    VAlert,
    VBtn,
    VExpansionPanelContent,
    VExpansionPanel,
    VIcon,
    VChip,
  },
  computed: {
    items() {
      return this.$store.getters.getClasses;
    },
    selected() {
      return this.$store.getters.getSelected;
    },
  },
  data() {
    return {
      isLoading: false,
      loadedOnce: false,
      headers: [
        { text: 'Title', value: 'title', align: 'left' },
        { text: 'Quarter', value: '', align: 'left' },
        { text: 'Class', value: '', align: 'left' },
        { text: 'Credits', value: 'cr', align: 'left' },
        { text: 'Instructor', value: 'instructor', align: 'left' },
        { text: 'Instruction Type', value: 'it', align: 'left' },
        { text: 'Instruction Method', value: 'im', align: 'left' },
        { text: 'Status', value: 'status', align: 'left' },
        { text: 'Enrolled', value: 'enrolled', align: 'left' },
        { text: 'CRN', value: 'crn', align: 'left' },
        { text: 'Time and Day', value: 'time_day', align: 'left' },
        { text: 'Add', value: '', align: 'left' },
      ],
    };
  },
  methods: {
    async loadListing() {
      this.isLoading = true;
      await this.$store.dispatch(UPDATE_CLASSES);
      this.isLoading = false;
    },
    removeFromSelected(index) {
      this.$store.dispatch(REMOVE_FROM_SELCTED, this.selected[index].crn);
    },
  },
  mounted() {
    EventBus.$on('refresh-field', () => {
      this.loadListing();
    });
    EventBus.$on('refresh-listing', () => {
      this.loadListing();
    });
  },
};
</script>

<style>

</style>
