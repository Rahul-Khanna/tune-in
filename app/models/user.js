// app/models/user.js
// load the things we need
var mongoose = require('mongoose');
var bcrypt   = require('bcrypt-nodejs');

// define the schema for our user model
var userSchema = mongoose.Schema({

    user            : {
        id        : mongoose.Schema.Types.ObjectId,

        spotifyInfo     : {
            token       : String,
            email       : String,
            userName    : String,
            active      : Boolean

        },
        soundcloudInfo  : {
            token       : String,
            email       : String,
            userName    : String,
            active      : Boolean
        },

        percOfTopArtists: { type: Number, min: 0, max: 100 },

        possibleArtists : [
            {
                artistId    : mongoose.Schema.Types.ObjectId,
                score       : {type: Number}
            }
        ],

        following: [mongoose.Schema.Types.ObjectId],

        newNotifications: [mongoose.Schema.Types.ObjectId],

        saveSongs: [mongoose.Schema.Types.ObjectId],

        timeStamp: {type: Date, default: Date.now},

        lastLogin: {type: Date}
    }
});

// methods ======================
// generating a hash
userSchema.methods.generateHash = function(password) {
    return bcrypt.hashSync(password, bcrypt.genSaltSync(8), null);
};

// checking if password is valid
userSchema.methods.validPassword = function(password) {
    return bcrypt.compareSync(password, this.local.password);
};

// create the model for users and expose it to our app
module.exports = mongoose.model('User', userSchema);