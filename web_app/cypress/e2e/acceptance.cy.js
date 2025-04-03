describe('Home Page Navigation', () => {
  it('should display register and login buttons', () => {
    cy.visit('http://localhost:3000'); // Adjust URL if needed

    cy.contains('Register').should('exist');
    cy.contains('Log In').should('exist');
  });

  it('should navigate to the register page', () => {
    cy.visit('http://localhost:3000');
    cy.contains('Register').click();
    cy.url().should('include', '/register');
  });

  it('should navigate to the login page', () => {
    cy.visit('http://localhost:3000');
    cy.contains('Log In').click();
    cy.url().should('include', '/login');
  });
});
