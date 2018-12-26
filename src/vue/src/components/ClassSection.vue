<template>
    <tr>
        <td>{{ classSection }}</td>
    </tr>
</template>

<script>
export default {
  name: 'ClassInfo',
  params: {
    classSection: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style>

</style>
