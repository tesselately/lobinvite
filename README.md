# lobinvite #

Add invitation codes and Steam friend invitations to your lobste.rs site.

This app works by synthesizing lobste.rs invitations and having the invited
visitor redeem them immediately. The lobste.rs site will show all self-invited
users to be invited by user #1 (presumably you). The method a lobste.rs member
uses to self-invite is recorded in the lobste.rs invitation's `memo` field.

As written this requires your lobste.rs site to use PostgreSQL for its database.


## To configure ##

Copy the `lobinvite.conf.example` file to `lobinvite.conf` and customize its
settings for your site. Run lobinvite with the `LOBINVITE_SETTINGS` environment
variable set to the path to `lobinvite.conf`:

    $ LOBINVITE_SETTINGS=./lobinvite.conf python lobinvite.py

Set up your site so `/join` on your lobste.rs site is forwarded to the
lobinvite app instead of lobste.rs. Use invitation codes by sending people the
link to the invitations page with `/join?code=invitationcode` appended.
