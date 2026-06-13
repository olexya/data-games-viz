<script>
	import '@evidence-dev/tailwind/fonts.css';
	import '../app.css';
	import { EvidenceDefaultLayout } from '@evidence-dev/core-components';
	import { showQueries } from '@evidence-dev/component-utilities/stores';
	import { onMount } from 'svelte';
	export let data;

	// Trace d'audit (aperçu des requêtes « X records with Y properties ») masquée
	// par défaut ; bouton ci-dessous pour l'afficher / la masquer.
	onMount(() => showQueries.set(false));
</script>

<EvidenceDefaultLayout {data} hideHeader={true} hideSidebar={true} hideTOC={true}>
	<div slot="content">
		<div class="flex justify-end mb-3">
			<button
				type="button"
				class="text-xs px-2 py-1 rounded border border-gray-300 text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition"
				on:click={() => showQueries.update((v) => !v)}
			>
				{$showQueries ? "🙈 Masquer la trace d'audit" : "🔎 Afficher la trace d'audit"}
			</button>
		</div>
		<slot />
	</div>
</EvidenceDefaultLayout>
