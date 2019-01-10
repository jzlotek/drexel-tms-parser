<template>
    <div class="o-select__wrapper">
      <div class="spinner__wrapper" v-if="isLoading">
        <Spinner/>
      </div>
        <v-flex xs12 sm6 d-flex v-if="hasChildren" @refresh="refresh">
            <v-autocomplete
              :disabled="isLoading"
              :items="fields"
              :label="fieldName"
              v-model="value">
              </v-autocomplete>
        </v-flex>
        <p v-else>{{ fieldName }} has no elements</p>
    </div>
</template>

<script>
import axios from 'axios';
import EventBus from '../../EventBus';
import Spinner from '../Spinner';
import { CLEAR_QUERY, ADD_TO_QUERY } from '../../store';

export default {
  name: 'SearchDropdown',
  components: {
    Spinner,
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
    }
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
    async dispatchUpdate() {
      if (this.clearQuery) {
        this.$store.dispatch(CLEAR_QUERY);
      }

      const obj = {};
      obj[`${this.queryParam}`] = this.value;
      this.$store.commit(ADD_TO_QUERY, obj);

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
