<template>
    <div class="o-select__wrapper">
      <div class="spinner__wrapper" v-if="isLoading">
        <Spinner/>
      </div>
        <v-flex xs12 sm6 d-flex v-if="hasChildren" @refresh="refresh">
            <v-select
              :disabled="isLoading"
              :items="fields.data"
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
      required: true
    }
  },
  data() {
    return {
      fields: [],
      isLoading: false,
      value: undefined,
      query: {},
    };
  },
  computed: {
    hasChildren() {
      return this.fields.data && this.fields.data.length > 0;
    },
  },
  methods: {
    async refresh() {
      let fields;
      this.isLoading = true;
      try {
        let queryParams = '';
        const L = Object.entries(this.query).length;
        let i = 0;
        if (L > 0){
          queryParams = '?';
          Object.entries(this.query).forEach(entry => {
            let param = `${entry[0]}=${entry[1]}`;
            if (i > 0) {
              queryParams += '&';
            }
            queryParams += param;
            i++;
          })
        }
        console.log(queryParams)
        fields = await axios.get(this.apiEndpoint + queryParams);
        this.fields = fields;
      } catch (error) {
        this.fields = [];
      }
      this.isLoading = false;
    },
    dispatchUpdate() {
      this.affectedFields.forEach((field) => {
        let obj = {};
        obj[`${this.queryParam}`] = this.value;
        EventBus.$emit('refresh-field', {field: field, q: obj});
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
      if (event.field === this.fieldName) {
        this.query = Object.assign(this.query, event.q);
        this.refresh();
      }
    });
    this.refresh();
  },
};
</script>

<style>

</style>
