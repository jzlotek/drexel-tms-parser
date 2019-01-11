<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="items"
      :loading="isLoading"
      class="elevation-1"
    >
      <v-progress-linear slot="progress" color="red" indeterminate/>
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
          <v-btn :href="item.crnLink" target="_blank">{{ item.crn }}</v-btn>
        </div>
        <v-card>
          <p class="text-xs-left">{{ item.course.title }}</p><br/>
          <p class="text-xs-center">{{ item.course.sc }}</p><br/>
          <p class="text-xs-center">{{ item.course.cn }}</p><br/>
          <p class="text-xs-center">{{ item.sec }}</p><br/>
          <p class="text-xs-center">{{ item.course.cr }}</p><br/>
          <p class="text-xs-center">{{ item.instructor }}</p><br/>
          <p class="text-xs-center">{{ item.course.it }}</p><br/>
          <p class="text-xs-center">{{ item.course.im }}</p>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </div>
</template>

<script>
import EventBus from '../EventBus';
import { UPDATE_CLASSES, REMOVE_FROM_SELCTED } from '../store/constants';
/* webpackChunkName: "class-listing-row" */
const ClassListingRow = () => import('./ClassListingRow');
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
/* webpackChunkName: "v-expansion-panel-card" */
const VCard = () => import('vuetify/es5/components/VCard/VCard');

export default {
  name: 'ClassListing',
  components: {
    ClassListingRow,
    VDataTable,
    VProgressLinear,
    VAlert,
    VBtn,
    VExpansionPanelContent,
    VExpansionPanel,
    VCard,
    VIcon,
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
        { text: 'Subject Code', value: 'sc', align: 'center' },
        { text: 'Course Number', value: 'cn', align: 'center' },
        { text: 'Section', value: 'sec', align: 'center' },
        { text: 'Credits', value: 'cr', align: 'center' },
        { text: 'Instructor', value: 'instructor', align: 'center' },
        { text: 'Instruction Type', value: 'it', align: 'center' },
        { text: 'Instruction Method', value: 'im', align: 'center' },
        { text: 'Status', value: 'status', align: 'center' },
        { text: 'Enrolled', value: 'enrolled', align: 'center' },
        { text: 'CRN', value: 'crn', align: 'center' },
        { text: 'Time and Day', value: 'time_day', align: 'center' },
        { text: 'Add', value: '', align: 'center' },
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
  },
};
</script>

<style>

</style>
