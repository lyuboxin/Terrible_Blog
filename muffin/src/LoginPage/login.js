import React, { Component } from 'react';

class Login extends Component {
    constructor(props){
        super(props);

        this.state = {
            username: '',
            password: '',
            submitted: false
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(e) {
        const {name, value} = e.target;
        this.setState({[name]: value});

    }

    handleSubmit(e) {
        e.preventDefault();

        this.setState({submitted: true});
        const{username, password} = this.state;
        
    }

    render() { 
        return (  );
    }
}
 
export default Login;