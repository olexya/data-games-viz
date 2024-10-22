<script>
	import '@evidence-dev/tailwind/fonts.css';
	import '../app.css';
	// import './app.css';
	import { EvidenceDefaultLayout } from '@evidence-dev/core-components';
	export let data;
</script>

<EvidenceDefaultLayout {data} neverShowQueries={true} hideHeader={true} hideSidebar={true} hideTOC={true}>
	<slot slot="content" />
</EvidenceDefaultLayout>
