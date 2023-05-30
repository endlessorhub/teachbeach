class CompanyService {
    getLink(profile) {
        return `/company/${profile.slug}`
    }
}

export default new CompanyService()