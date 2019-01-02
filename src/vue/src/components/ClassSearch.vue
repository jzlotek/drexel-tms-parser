<template>
    <div>
      <SearchDropdown fieldName="test" apiEndpoint="/api/1"/>
      <SearchDropdown fieldName="test" apiEndpoint="/api/2"/>
      <SearchDropdown fieldName="test" apiEndpoint="/api/3"/>
      <SearchDropdown fieldName="test" apiEndpoint="/api/4"/>
      <button @click="refreshChildren()">Refresh</button>
      <br/>
      <button @click="executeQuery()">Execute Query</button>
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
    executeQuery() {
      EventBus.$emit('execute-query');
    },
  },
};
</script>
