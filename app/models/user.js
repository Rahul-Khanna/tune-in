// app/models/user.js
// load the things we need
var mongoose = require('mongoose');
var bcrypt   = require('bcrypt-nodejs');


var userSchema = mongoose.Schema({
    email: String,
    spotifyInfo: {
        token       : String,
        refresh     : String,
        id          : String,
        userName    : String,
        active      : Boolean
    },
    soundCloudInfo: {
        token       : String,
        refresh     : String,
        id          : String,
        userName    : String,
        active      : Boolean
    }, 
    
    percOfTopArtists: { type: Number, min: 0, max: 100, default: 100},

    possibleArtists : [
        {
            artistId    : mongoose.Schema.Types.ObjectId,
            score       : {type: Number},
        }
    ],

    following: [String],

    newNotifications: [mongoose.Schema.Types.ObjectId],

    saveSongs: [mongoose.Schema.Types.ObjectId],

    timeStamp: {type: Date, default: Date.now},

    lastLogin: {type: Date}
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