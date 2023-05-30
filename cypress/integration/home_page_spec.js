describe('The Home Page', () => {
    it('successfully loads', () => {
        cy.visit('/')
    })

    it('checking viewports', () => {
        cy.visit('/')
        cy.get('.app-toolbar').should('be.visible')

        cy.viewport(2999, 2999)
        cy.get('[data-desktop-nav-addclass]').should('be.visible')
        cy.get('[data-mobile-nav-menu-icon]').should('not.be.visible')
        cy.get('[data-desktop-search-topic]').should('be.visible')
        cy.get('[data-mobile-search-topic]').should('not.be.visible')

        cy.viewport('ipad-2')
        cy.get('[data-desktop-nav-addclass]').should('not.be.visible')
        cy.get('[data-mobile-nav-menu-icon]').should('be.visible')
        cy.get('[data-desktop-search-topic]').should('be.visible')
        cy.get('[data-mobile-search-topic]').should('not.be.visible')

        cy.viewport('iphone-x')
        cy.get('[data-desktop-nav-addclass]').should('not.be.visible')
        cy.get('[data-mobile-nav-menu-icon]').should('be.visible')
        cy.get('[data-desktop-search-topic]').should('not.be.visible')
        cy.get('[data-mobile-search-topic]').should('be.visible')

        cy.viewport('iphone-xr')
        cy.get('[data-desktop-nav-addclass]').should('not.be.visible')
        cy.get('[data-mobile-nav-menu-icon]').should('be.visible')
        cy.get('[data-desktop-search-topic]').should('not.be.visible')
        cy.get('[data-mobile-search-topic]').should('be.visible')

        cy.viewport('macbook-15')
        cy.get('[data-desktop-nav-addclass]').should('be.visible')
        cy.get('[data-mobile-nav-menu-icon]').should('not.be.visible')
        cy.get('[data-desktop-search-topic]').should('be.visible')
        cy.get('[data-mobile-search-topic]').should('not.be.visible')
    })
})