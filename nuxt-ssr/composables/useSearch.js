import { useRouter } from '#app';

export const useSearch = () => {
    const router = useRouter();

    const slugify = (text) => {
        if (!text) return '';
        return text
            .toString()
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/\s+/g, '-')
            .replace(/[^\w\-]+/g, '');
    };

    const handleSelection = (selection) => {
        const { item, type } = selection;

        if (type === 'listings' && item.id) {
            const slug = slugify(item.listingName);
            router.push(`/listing/view/${item.id}/${slug}`);
        } else if (type === 'venues' && item.id) {
            const slug = slugify(item.venueName);
            router.push(`/profile/venue/${item.id}/${slug}`);
        } else if (type === 'producers' && item.id) {
            const slug = slugify(item.producerName);
            router.push(`/profile/producer/${item.id}/${slug}`);
        } else if (type === 'users' && item.id) {
            const slug = slugify(item.username);
            router.push(`/profile/user/${item.id}/${slug}`);
        } else if ((type === 'Any' || type === 'FullSearch') && item.name) {
            const query = encodeURIComponent(item.name.trim().replace(/\//g, ''));
            router.push(`/search/${query}`);
        }
    };

    return {
        handleSelection,
    };
};