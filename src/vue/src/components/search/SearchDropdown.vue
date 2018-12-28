<template>
    <div class="o-select__wrapper">
      <div class="spinner__wrapper" v-if="isLoading">
        <Spinner/>
      </div>
        <div class="o-select__inner" v-if="hasChildren" @refresh="refresh">
            <select
                :name="name" id=""
                v-for="(field, index) in fields"
                :key="index"
                :disabled="isLoading"
            >
                <option :value="field.value">
                    {{ field.name }}
                </option>
            </select>
        </div>
        <p v-else>{{ name }} has no elements</p>
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
    name: {
      type: String,
      required: true,
    },
    apiEndpoint: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      fields: [],
      isLoading: false,
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
  },
  mounted() {
    EventBus.$on('refresh-search', () => {
      this.refresh();
    });
  },
};
</script>

<style>

</style>
