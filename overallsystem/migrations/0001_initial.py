# Generated by Django 2.1.5 on 2019-01-23 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Playlists',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlist_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistTracks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track', models.CharField(max_length=50, null=True)),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overallsystem.Playlists')),
            ],
        ),
        migrations.CreateModel(
            name='Profiles',
            fields=[
                ('user', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('acousticness', models.FloatField(null=True)),
                ('danceability', models.FloatField(null=True)),
                ('energy', models.FloatField(null=True)),
                ('instrumentalness', models.FloatField(null=True)),
                ('key', models.FloatField(null=True)),
                ('liveness', models.FloatField(null=True)),
                ('loudness', models.FloatField(null=True)),
                ('speechiness', models.FloatField(null=True)),
                ('tempo', models.FloatField(null=True)),
                ('valence', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tracks',
            fields=[
                ('track', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('listens', models.IntegerField(default=0)),
                ('ratings', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserFaves',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overallsystem.Tracks')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overallsystem.Profiles')),
            ],
        ),
        migrations.CreateModel(
            name='UserListens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listen_duration', models.IntegerField()),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overallsystem.Tracks')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overallsystem.Profiles')),
            ],
        ),
        migrations.AddField(
            model_name='playlists',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overallsystem.Profiles'),
        ),
        migrations.AlterUniqueTogether(
            name='userfaves',
            unique_together={('user', 'track')},
        ),
    ]
