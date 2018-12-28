<template>
    <div>
        <SearchDropdown name="test" apiEndpoint="http://localhost:8080/api/1"></SearchDropdown>
        <SearchDropdown name="test" apiEndpoint="http://localhost:8080/api/2"></SearchDropdown>
        <SearchDropdown name="test" apiEndpoint="http://localhost:8080/api/3"></SearchDropdown>
        <SearchDropdown name="test" apiEndpoint="http://localhost:8080/api/4"></SearchDropdown>
        <button @click="refreshChildren()">Refresh</button>
    </div>
</template>
<script>
import SearchDropdown from './search/SearchDropdown';
import EventBus from '../EventBus';

export default {
  name: 'ClassSearch',
  components: {
    SearchDropdown,
  },
  methods: {
    refreshChildren() {
      EventBus.$emit('refresh-search');
    },
  },
};
</script>
