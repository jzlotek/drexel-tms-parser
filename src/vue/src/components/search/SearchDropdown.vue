<template>
    <div class="o-select__wrapper">
      <div class="spinner__wrapper" v-if="isLoading">
        <Spinner/>
      </div>
        <div class="o-select__inner" v-if="hasChildren" @refresh="refresh">
            <select
                class="o-select__dropdown"
                v-model="value"
                :disabled="isLoading"
            >
                <option v-for="(field, index) in fields" :key="index" :value="field.value">
                    {{ field.name }}
                </option>
            </select>
        </div>
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
        fields = await axios.get(this.apiEndpoint);
        this.fields = fields;
      } catch (error) {
        this.fields = [];
      }
      this.isLoading = false;
    },
    dispatchUpdate() {
      this.affectedFields.forEach((field) => {
        EventBus.$emit('refresh-field', field);
      });
    },
  },
  watch: {
    value() {
      this.dispatchUpdate();
    },
  },
  mounted() {
    EventBus.$on('refresh-search', (fields) => {
      if (fields && fields.contains(this.fieldName)) {
        this.refresh();
      }
    });
    EventBus.$on('refresh-field', (field) => {
      if (field === this.fieldName) {
        this.refresh();
      }
    });
  },
};
</script>

<style>

</style>
