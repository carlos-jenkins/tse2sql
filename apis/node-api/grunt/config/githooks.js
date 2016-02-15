module.exports = {
    all: {
        options: {
            template: 'grunt/etc/git-hooks/pre-commit.js'
        },
        'pre-commit': 'jshint'
    }
};