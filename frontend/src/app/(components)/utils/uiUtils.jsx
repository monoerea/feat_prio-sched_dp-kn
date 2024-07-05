export function dynamicGrouper(features) {
    const maxFeaturesPerGroup = 3;
    const groupedFeatures = [];
    let i = 0;

    while (i < features.length) {
        // Generate a random number of features for this group between 1 and maxFeaturesPerGroup
        const remainingFeatures = features.length - i;
        const numberOfFeaturesInGroup = Math.min(Math.floor(Math.random() * maxFeaturesPerGroup) + 1, remainingFeatures);

        // Create the group with the determined number of features
        const group = features.slice(i, i + numberOfFeaturesInGroup).map((feature, index) => ({
            id: feature,
            name: feature,
            group: Math.floor(i / maxFeaturesPerGroup) + 1,
            type: 'input',
            placeholder: `Enter value`
        }));
        groupedFeatures.push(...group);
        i += numberOfFeaturesInGroup;
    }

    return groupedFeatures;
}
