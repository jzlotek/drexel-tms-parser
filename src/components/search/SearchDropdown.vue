<template>
    <div class="o-select__wrapper">
      <v-card xs12 sm6 d-flex @refresh="refresh">
        <v-autocomplete
          :disabled="isLoading"
          :items="fields"
          :label="fieldName"
          v-model="value"
          :loading="isLoading">
            <v-progress-linear slot="progress" color="red" indeterminate/>
            <div slot="no-data">{{ fieldName }} has no elements for the selected parameters</div>
          </v-autocomplete>
        </v-card>
    </div>
</template>

<script>
import axios from 'axios';
import EventBus from '../../EventBus';
import { CLEAR_QUERY, ADD_TO_QUERY } from '../../store/constants';

/* webpackChunkName: "v-auto-complete" */
const VAutocomplete = () => import('vuetify/es5/components/VAutocomplete/VAutocomplete');
/* webpackChunkName: "v-progress-linear" */
const VProgressLinear = () => import('vuetify/es5/components/VProgressLinear/VProgressLinear');
/* webpackChunkName: "v-card" */
const VCard = () => import('vuetify/es5/components/VCard/VCard');

export default {
  name: 'SearchDropdown',
  components: {
    VAutocomplete,
    VProgressLinear,
    VCard,
  },
  props: {
    fieldName: {
      type: String,
      required: true,
    },
    fieldSlug: {
      type: String,
      required: true,
    },
    apiEndpoint: {
      type: String,
      required: true,
    },
    affectedFields: {
      type: Array,
      required: true,
    },
    queryParam: {
      type: String,
      required: true,
    },
    clearQuery: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      fields: [],
      isLoading: false,
      value: undefined,
    };
  },
  computed: {
    hasChildren() {
      return this.fields && this.fields.length > 0;
    },
    queryParams() {
      return this.$store.getters.getQueryString;
    },
  },
  methods: {
    async refresh() {
      let fields;
      this.isLoading = true;
      try {
        fields = await axios.get(`${this.apiEndpoint}${this.queryParams}`);
        this.fields = fields.data;
      } catch (error) {
        this.fields = [];
      }
      this.isLoading = false;
    },
    dispatchUpdate() {
      if (this.clearQuery) {
        this.$store.dispatch(CLEAR_QUERY);
      }

      const obj = {};
      obj[`${this.queryParam}`] = this.value;
      this.$store.dispatch(ADD_TO_QUERY, obj);

      this.affectedFields.forEach((field) => {
        EventBus.$emit('refresh-field', { fieldSlug: field });
      });
    },
  },
  watch: {
    value() {
      this.dispatchUpdate();
    },
  },
  mounted() {
    EventBus.$on('refresh-field', (event) => {
      if (event.fieldSlug === this.fieldSlug) {
        this.refresh();
      }
    });
    this.refresh();
  },
};
</script>

<style>

</style>
