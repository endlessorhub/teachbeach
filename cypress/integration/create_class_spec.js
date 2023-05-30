describe('Creating class', () => {
    const hash = Number(new Date().getTime()).toString(36)
    before(() => {
         cy.visit('/teachers/start')
    })
    it('successfully loads', () => {
        cy.get('button').contains('Next').should('to.exist')
    })

    it('category select page', () => {
        cy.contains('Select or create a topic').should('to.exist')
    })

    it('choose first category', () => {
        cy.contains('Sports').parent().click()
        cy.get('.v-menu__content:visible').contains('Kayak').click()
        cy.get('.v-chip__content').contains('Kayak').should('to.exist')
    })

    it('choose second category', () => {
        cy.contains('Sports').parent().click()
        cy.get('.v-menu__content:visible').contains('Tennis').click()
        cy.get('.v-chip__content').contains('Tennis').should('to.exist')
    })

    it('choose third category', () => {
        cy.contains('Sports').parent().click()
        cy.get('.v-menu__content:visible').contains('Paddleboard').click()
        cy.get('.v-chip__content').contains('Paddleboard').should('to.exist')
    })

    it('choose fourth category', () => {
        cy.contains('Sports').parent().click()
        cy.get('.v-menu__content:visible').contains('Pickleball').click()
        cy.get('.v-chip__content').contains('Pickleball').should('not.to.exist')
    })

    it('go to the contact page', () => {
        cy.get('button').contains('Next').click()
        cy.contains('Please register to post classes').should('to.exist')
    })

    it('missing first name', () => {
        cy.get('input[name="first_name"]').click()
        cy.get('input[name="last_name"]').type(`Svistoplyasov${hash}`)
        cy.contains('Name is required').should('be.visible')
    })

    it('missing email', () => {
        cy.get('input[name="email"]').click()
        cy.get('input[name="first_name"]').type(`Innokentiy${hash}`)
        cy.contains('E-mail is required').should('be.visible')
    })

    it('wrong email format', () => {
        cy.get('input[name="email"]').type(`Innosvist${hash}@greatmail`)
        cy.contains('Must be valid e-mail').should('be.visible')
    })

    it('correct email format', () => {
        cy.get('input[name="email"]').type(`.con`)
        cy.contains('Must be valid e-mail').should('not.be.visible')
    })

    it('password repeat check fails', () => {
        cy.get('input[name="password"]').type(`11111111`)
        cy.get('input[name="repeat_password"]').type(`11111112`)
        cy.contains('Repeated password does not match original').should('be.visible')
    })
    it('password repeat fix', () => {
        cy.get('input[name="repeat_password"]').type(`{backspace}1`)
        cy.contains('Repeated password does not match original').should('not.be.visible')
    })

    it('city autocomplete', () => {
        cy.contains('City').parent().find('input').click().type(`st peters`, {delay: 50}).wait(1000)
            .type('{downarrow}{enter}')
        cy.contains('City').parent().find('input').should('to.have.value', 'St. Petersburg, FL, USA')
    })

    it('form errors check', () => {
        cy.contains('Start Teaching').closest('button').click()
        cy.contains('You must confirm you are over 18 years old').should('be.visible')
        cy.contains('Phone is required').should('be.visible')
    })

    it('form errors fixed', () => {
        cy.get('input[name="phone"]').type(`123123123`)
        cy.get('.v-input--checkbox').contains('I am 18 years old or older').click()
        cy.contains('You must confirm you are over 18 years old').should('not.be.visible')
        cy.contains('Phone is required').should('not.be.visible')

    })

    it('user registered, next is create profile', () => {
        cy.contains('Start Teaching').closest('button').click()
        cy.contains('Create your profile').should('be.visible')
    })

    it('fill in, no errors', () => {
        cy.contains('What makes you stand-out as a teacher').parent().find('textarea').type("I'm unique teacher with perfect skills")
        cy.contains('Areas of speciality').parent().find('input[type=text]').type('paddle fighting{enter}rocket jump{enter}')
        cy.contains('What makes you stand-out as a teacher').parent().find('textarea').should('to.have.value', "I'm unique teacher with perfect skills")
        cy.get('.v-chip').contains('paddle fighting').should('be.visible')
        cy.get('.v-chip').contains('rocket jump').should('be.visible')
    })

})