<template>
    <div class="o-select__wrapper">
      <div class="spinner__wrapper" v-if="isLoading">
        <Spinner/>
      </div>
        <v-flex xs12 sm6 d-flex v-if="hasChildren" @refresh="refresh">
            <v-select
              :disabled="isLoading"
              :items="fields"
              :label="fieldName"
              v-model="value">
              </v-select>
        </v-flex>
        <p v-else>{{ fieldName }} has no elements</p>
    </div>
</template>

<script>
import axios from 'axios';
import EventBus from '../../EventBus';
import Spinner from '../Spinner';

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
  },
  methods: {
    async refresh() {
      let fields;
      this.isLoading = true;
      try {
        let queryParams = '';
        const L = Object.entries(this.$store.state.query).length;
        let i = 0;
        if (L > 0) {
          queryParams = '?';
          Object.entries(this.$store.state.query).forEach((entry) => {
            const param = `${entry[0]}=${entry[1]}`;
            if (i > 0) {
              queryParams += '&';
            }
            queryParams += param;
            i += 1;
          });
        }
        fields = await axios.get(this.apiEndpoint + queryParams);
        this.fields = fields.data;
      } catch (error) {
        this.fields = [];
      }
      this.isLoading = false;
    },
    async dispatchUpdate() {
      if (this.clearQuery) {
        this.$store.commit('clearQuery');
      }
      const obj = {};
      obj[`${this.queryParam}`] = this.value;
      this.$store.commit('addToQuery', obj);
      this.affectedFields.forEach((field) => {
        EventBus.$emit('refresh-field', { fieldName: field });
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
      if (event.fieldName === this.fieldName) {
        this.refresh();
      }
    });
    this.refresh();
  },
};
</script>

<style>

</style>
